document.addEventListener('DOMContentLoaded', () => {
    const serverUrl = 'http://127.0.0.1:5000/fetch';
    const dataTable = document.getElementById('data-table').getElementsByTagName('tbody')[0];
    let data = [];

    async function fetchData() {
        try {
            const response = await fetch(`${serverUrl}?n=15`);
            if (response.ok) {
                data = await response.json();
                console.log('Fetched data:', data); // Log fetched data for debugging
                displayData();
            } else {
                console.error('Failed to fetch data from the server. Status:', response.status);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    function displayData() {
        dataTable.innerHTML = '';
        data.forEach(activity => {
            const row = dataTable.insertRow();
            Object.values(activity).forEach(value => {
                const cell = row.insertCell();
                cell.textContent = value !== null ? value : '';
            });
        });
    }

    function downloadJSON() {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'data.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    function downloadCSV() {
        if (data.length === 0) return;
        const csvData = [];
        const headers = Object.keys(data[0]).join(',');
        csvData.push(headers);
        data.forEach(activity => {
            const row = Object.values(activity).join(',');
            csvData.push(row);
        });
        const blob = new Blob([csvData.join('\n')], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'data.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    function printToConsole() {
        console.log(data);
    }

    document.getElementById('download-json').addEventListener('click', downloadJSON);
    document.getElementById('download-csv').addEventListener('click', downloadCSV);
    document.getElementById('print-console').addEventListener('click', printToConsole);

    fetchData();
});
