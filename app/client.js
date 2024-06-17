const net = require('net');
const fs = require('fs');

const serverAddress = '/tmp/socket_file';
let client = new net.Socket();

function connectClient() {
    client.connect(serverAddress, () => {
        console.log('Connected to server');
        promptUser();
    });
}

function setupClientHandlers() {
    client.on('data', (data) => {
        console.log(`Server response: ${data}`);
        promptUser();
    });

    client.on('close', () => {
        console.log('Connection closed');
        client.removeAllListeners();
        client = new net.Socket();
        setupClientHandlers();
        connectClient();
    });

    client.on('error', (err) => {
        console.error(`Socket error: ${err.message}`);
        client.destroy();
        client = new net.Socket();
        setupClientHandlers();
        connectClient();
    });
}

function promptUser() {
    process.stdout.write('Enter request file number (or "exit" to quit): ');
}

setupClientHandlers();
connectClient();

process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', (data) => {
    const input = data.trim();
    if (input === 'exit') {
        client.end();
        process.exit();
    } else {
        const filePath = `../api/request${input}.json`;
        fs.readFile(filePath, 'utf8', (err, content) => {
            if (err) {
                console.error(`File ${filePath} not found`);
                promptUser();
            } else {
                client.write(content);
            }
        });
    }
});
