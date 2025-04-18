import { spawn } from 'child_process';

// Start Streamlit application using "python -m streamlit run streamlit_app.py"
const streamlit = spawn('python', ['-m', 'streamlit', 'run', 'streamlit_app.py']);

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
