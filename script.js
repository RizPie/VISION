let isMuted = false;

function playSound() {
    if (isMuted) return;
    const audio = new Audio('message-envoye-iphone-apple-391098.mp3');
    audio.volume = 0.05; // Much lower volume
    audio.play().catch(e => console.log('Audio play failed:', e));
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('send-button').addEventListener('click', sendMessage);
    document.getElementById('user-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    document.getElementById('mute-button').addEventListener('click', toggleMute);

    // Fetch user info
    fetch('/user')
        .then(response => response.json())
        .then(data => {
            if (data.name) {
                document.getElementById('user-name').textContent = data.name;
            }
        })
        .catch(error => console.log('Error fetching user:', error));
});

function toggleMute() {
    isMuted = !isMuted;
    const icon = document.getElementById('mute-icon');
    icon.textContent = isMuted ? '🔇' : '🔊';
    console.log('Mute toggled:', isMuted);
    if (!isMuted) {
        playSound(); // Test sound
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    const model = document.getElementById('model-select').value;

    addMessage('user', message);
    playSound(); // Send sound
    input.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message, model: model })
    })
    .then(response => response.json())
    .then(data => {
        addMessage('assistant', data.response);
        playSound(); // Receive sound
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('assistant', 'Sorry, there was an error.');
        // No sound for error, or different
    });
}

function addMessage(role, content) {
    const history = document.getElementById('chat-history');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.innerHTML = marked.parse(content);
    history.appendChild(messageDiv);
    history.scrollTop = history.scrollHeight;
}