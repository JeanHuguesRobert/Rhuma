const { spawn } = require('child_process');

// Start Streamlit application
const streamlit = spawn('streamlit', ['run', 'streamlit_app.py']);

// Stream output to console
streamlit.stdout.on('data', (data) => {
    process.stdout.write(data.toString());
});

streamlit.stderr.on('data', (data) => {
    process.stderr.write(data.toString());
});

streamlit.on('error', (error) => {
    console.error(`Error: ${error}`);
});

streamlit.on('close', (code) => {
    console.log(`Streamlit process exited with code ${code}`);
});
