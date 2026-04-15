-- Insert test user
INSERT INTO users (id, name, email, password, created_at)
VALUES (
    gen_random_uuid(),
    'Test User',
    'test@example.com',
    '$2b$12$dLRk2jRwzVDvrrsrny5VaOM3I.hcJj/p6SGE9MEwab5QTG2eRG1a6', -- password: password123
    NOW()
);

-- Insert project (linked to above user)
INSERT INTO projects (id, name, description, owner_id, created_at)
VALUES (
    gen_random_uuid(),
    'Sample Project',
    'Demo project for testing',
    (SELECT id FROM users WHERE email = 'test@example.com'),
    NOW()
);

-- Insert tasks
INSERT INTO tasks (id, title, description, status, project_id, assignee_id, created_at)
VALUES
(
    gen_random_uuid(),
    'Task 1 - Todo',
    'First task',
    'todo',
    (SELECT id FROM projects LIMIT 1),
    (SELECT id FROM users WHERE email = 'test@example.com'),
    NOW()
),
(
    gen_random_uuid(),
    'Task 2 - In Progress',
    'Second task',
    'in_progress',
    (SELECT id FROM projects LIMIT 1),
    (SELECT id FROM users WHERE email = 'test@example.com'),
    NOW()
),
(
    gen_random_uuid(),
    'Task 3 - Done',
    'Third task',
    'done',
    (SELECT id FROM projects LIMIT 1),
    (SELECT id FROM users WHERE email = 'test@example.com'),
    NOW()
);