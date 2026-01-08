const { spawn } = require('child_process');

const child = spawn('gemini', process.argv.slice(2), {
    stdio: 'inherit',
    shell: true
});

// Ignore resize errors
process.stdout.on('resize', () => {
    try {
        if (child.pid && !child.killed) {
            process.kill(child.pid, 0); // Check if alive
        }
    } catch (e) {
        // Ignore
    }
});

child.on('exit', (code) => {
    process.exit(code);
});