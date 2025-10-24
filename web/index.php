<?php
require 'vendor/autoload.php'; // if you installed MongoDB PHP library via Composer

$client = new MongoDB\Client("mongodb://localhost:27017");
$collection = $client->nyse_tracker->most_active;

$cursor = $collection->find([], ['limit' => 50]);
?>
<!DOCTYPE html>
<html>
<head>
    <title>Most Active Stocks - NYSE Tracker</title>
</head>
<body>
    <h1>Most Active Stocks</h1>
    <table border="1">
        <tr><th>Symbol</th><th>Name</th><th>Change</th><th>Volume</th><th>Timestamp</th></tr>
        <?php foreach ($cursor as $doc): ?>
        <tr>
            <td><?= $doc['Symbol'] ?? '' ?></td>
            <td><?= $doc['Name'] ?? '' ?></td>
            <td><?= $doc['Change'] ?? '' ?></td>
            <td><?= $doc['Volume'] ?? '' ?></td>
            <td><?= $doc['timestamp']->toDateTime()->format('Y-m-d H:i:s') ?></td>
        </tr>
        <?php endforeach; ?>
    </table>
</body>
</html>
