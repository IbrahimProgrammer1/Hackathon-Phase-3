// End-to-end user scenario tests
import { test, expect } from '@playwright/test';

// Test the complete user flow: login -> create task -> update task -> mark complete -> delete task
test.describe('User Flow Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('http://localhost:3000');
  });

  test('Complete task management flow', async ({ page }) => {
    // 1. User navigates to login page
    await page.getByRole('link', { name: 'Login' }).click();
    await expect(page).toHaveURL(/.*auth\/login/);

    // 2. User logs in
    await page.locator('#email-address').fill('test@example.com');
    await page.locator('#password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // 3. User is redirected to tasks page
    await expect(page).toHaveURL(/.*tasks/);

    // 4. User creates a new task
    await page.locator('#title').fill('Test Task');
    await page.locator('textarea').fill('Test task description');
    await page.getByRole('button', { name: 'Create Task' }).click();

    // 5. User sees the new task in the list
    await expect(page.getByText('Test Task')).toBeVisible();

    // 6. User updates the task
    await page.getByText('Edit').click();
    await page.locator('input').fill('Updated Task Title');
    await page.getByRole('button', { name: 'Save' }).click();

    // 7. User sees the updated task
    await expect(page.getByText('Updated Task Title')).toBeVisible();

    // 8. User marks task as complete
    await page.getByRole('button', { name: 'Mark Complete' }).click();

    // 9. User sees the task is marked complete
    await expect(page.getByText('✓ Completed')).toBeVisible();

    // 10. User deletes the task
    await page.getByRole('button', { name: 'Delete' }).click();
    await page.getByText('Are you sure you want to delete this task?');
    await page.getByRole('button', { name: 'OK' }).click(); // Confirm deletion

    // 11. User sees the task is removed
    await expect(page.getByText('Updated Task Title')).not.toBeVisible();
  });

  test('Authentication flow', async ({ page }) => {
    // 1. User navigates to tasks page without logging in
    await page.goto('http://localhost:3000/tasks');

    // 2. User is redirected to login page
    await expect(page).toHaveURL(/.*auth\/login/);

    // 3. User creates account
    await page.getByRole('link', { name: 'Register' }).click();
    await page.locator('#full-name').fill('Test User');
    await page.locator('#email-address').fill('newuser@example.com');
    await page.locator('#password').fill('password123');
    await page.getByRole('button', { name: 'Create Account' }).click();

    // 4. User is redirected to tasks page after registration
    await expect(page).toHaveURL(/.*tasks/);
  });

  test('Security: Cross-user access prevention', async ({ page, context }) => {
    // Create two users and verify they can't access each other's tasks
    // This would require creating multiple users and testing access between them
    // For now, this is a placeholder for the concept

    // Simulate user A logging in
    await page.goto('http://localhost:3000/auth/login');
    await page.locator('#email-address').fill('userA@example.com');
    await page.locator('#password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // User A creates a task
    await page.locator('#title').fill('User A Task');
    await page.getByRole('button', { name: 'Create Task' }).click();

    // Simulate user B logging in with a different context
    const userBContext = await context.browser().newContext();
    const userBPage = await userBContext.newPage();

    await userBPage.goto('http://localhost:3000/auth/login');
    await userBPage.locator('#email-address').fill('userB@example.com');
    await userBPage.locator('#password').fill('password123');
    await userBPage.getByRole('button', { name: 'Sign in' }).click();

    // User B should not see User A's task
    await expect(userBPage.getByText('User A Task')).not.toBeVisible();
  });
});