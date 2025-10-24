<?php
$mongoClient = new MongoDB\Client("mongodb://localhost:27017"); // Change URL to your MongoDB server
$database = $mongoClient->stock_database; // Change 'stock_database' to your database name
$collection = $database->most_active_stocks; // Change 'most_active_stocks' to your collection name

$result = $collection->find();

echo "<table border='1'>";
echo "<tr><th>Index</th><th>Symbol</th><th>Price (Intraday)</th><th>Change</th><th>Volume</th><th>Name</th></tr>";

foreach ($result as $document) {
    echo "<tr>";
    echo "<td>" . $document['Index'] . "</td>";
    echo "<td>" . $document['Symbol'] . "</td>";
    echo "<td>" . $document['Price (Intraday)'] . "</td>";
    echo "<td>" . $document['Change'] . "</td>";
    echo "<td>" . $document['Volume'] . "</td>";
    echo "<td>" . $document['Name'] . "</td>";
    echo "</tr>";
}

echo "</table>";
?>
