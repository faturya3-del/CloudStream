const { PeerServer } = require('peer');

const port = process.env.PORT || 9000;

const server = PeerServer({
    port: port,
    path: '/mirror',
    allow_discovery: true
});

console.log(`Server Cloud Signaling WebRTC aktif di port ${port}`);
