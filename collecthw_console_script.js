// CollectHW.com Table Extractor
// Press F12, go to Console tab, paste this entire code, and press Enter

(function() {
    let cars = [];
    let rowCount = 0;
    
    // Find all table rows (the cars are in table rows)
    const rows = document.querySelectorAll('table tbody tr, tr[class*="row"]');
    
    console.log('Found ' + rows.length + ' rows to process...');
    
    rows.forEach((row, index) => {
        try {
            // Get all cells in this row
            const cells = row.querySelectorAll('td');
            
            if (cells.length < 5) return; // Skip if not enough columns
            
            // Extract image
            const imgCell = row.querySelector('img');
            const imageUrl = imgCell ? imgCell.src : '';
            
            // Get text from each cell
            const cellTexts = Array.from(cells).map(cell => cell.textContent.trim());
            
            // Based on your screenshot, the columns appear to be:
            // Owned, Image, Col#, Series, Model Name, Year, Series, Color, Tampo, Wheel Type, Toy#, Assortment#, Case Letter, Notes, Exclusive, Value
            
            const modelName = cells[3] ? cells[3].textContent.trim() : '';
            const year = cells[4] ? cells[4].textContent.trim() : '';
            const series = cells[5] ? cells[5].textContent.trim() : '';
            const color = cells[6] ? cells[6].textContent.trim() : '';
            const tampo = cells[7] ? cells[7].textContent.trim() : '';
            const wheelType = cells[8] ? cells[8].textContent.trim() : '';
            const toyNumber = cells[9] ? cells[9].textContent.trim() : '';
            const notes = cells[12] ? cells[12].textContent.trim() : '';
            
            if (modelName && modelName !== '') {
                const car = {
                    id: 'hw-' + Date.now() + '-' + rowCount++,
                    name: modelName,
                    series: series,
                    year: year,
                    color: color,
                    manufacturer: 'Mattel',
                    category: series,
                    imageUrl: imageUrl,
                    notes: notes || tampo || '',
                    wheelType: wheelType,
                    toyNumber: toyNumber
                };
                
                cars.push(car);
            }
        } catch (e) {
            console.log('Error processing row ' + index + ':', e);
        }
    });
    
    if (cars.length === 0) {
        alert('No cars found! The page structure might be different than expected.\n\nTry scrolling down to load more cars, then run this again.');
        return;
    }
    
    // Create output
    const output = JSON.stringify(cars, null, 2);
    
    console.log('Successfully extracted ' + cars.length + ' cars!');
    console.log('Preview of first car:');
    console.log(cars[0]);
    
    // Try to copy to clipboard
    navigator.clipboard.writeText(output).then(() => {
        alert('✅ SUCCESS!\n\nExtracted ' + cars.length + ' Hot Wheels cars!\n\nThe data has been copied to your clipboard.\n\nNow:\n1. Open the collecthw_extractor.html file\n2. Paste into the text area\n3. Click "Download as JavaScript"');
    }).catch(() => {
        // Fallback: open in new window
        const newWindow = window.open('', '_blank');
        newWindow.document.write('<html><head><title>Extracted Cars</title></head><body>');
        newWindow.document.write('<h2>Extracted ' + cars.length + ' cars - Copy this JSON:</h2>');
        newWindow.document.write('<button onclick="navigator.clipboard.writeText(document.querySelector(\'pre\').textContent).then(() => alert(\'Copied!\'))">Copy to Clipboard</button>');
        newWindow.document.write('<pre style="background: #f5f5f5; padding: 20px; overflow: auto;">' + output + '</pre>');
        newWindow.document.write('</body></html>');
        alert('Data opened in new window. Copy it from there!');
    });
})();
