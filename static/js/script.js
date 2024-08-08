let chart;

        function toggleForm() {
            const formContainer = document.getElementById('formContainer');
            const resultContainer = document.getElementById('resultContainer');
            
            if (formContainer.style.display === 'none' || formContainer.style.display === '') {
                formContainer.style.display = 'block';
                resultContainer.style.display = 'none';
            } else {
                formContainer.style.display = 'none';
                resultContainer.style.display = 'none';
            }
        }

        function formatTime(isoString) {
            const date = new Date(isoString);
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }

        function createChart(labels, data) {
            const ctx = document.getElementById('energyChart').getContext('2d');
            
            if (chart) {
                chart.destroy();
            }

            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels.map(formatTime),
                    datasets: [{
                        label: 'Energy Consumption (Wh)',
                        data: data,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Energy Consumption (Wh)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Energy Consumption Trend'
                        }
                    }
                }
            });
        }

        async function handleFormSubmit(event) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log("Server response:", result);

                    const predictionResultElement = document.getElementById('predictionResult');
                    const parameterInfoElement = document.getElementById('parameterInfo');

                    predictionResultElement.innerHTML = `<h2>${result.text}</h2>`;

                    parameterInfoElement.innerHTML = '<h3>Parameter Information</h3>';
                    for (const [key, value] of Object.entries(result)) {
                        if (key !== 'prediction' && key !== 'text' && key !== 'timestamp') {
                            parameterInfoElement.innerHTML += `<p>${key}: ${value}</p>`;
                        }
                    }

                    // Hide form and show results
                    document.getElementById('formContainer').style.display = 'none';
                    document.getElementById('resultContainer').style.display = 'block';

                    // Fetch and update chart
                    fetchAndUpdateChart();
                } else {
                    console.error('Error:', response.statusText);
                    alert('Error: ' + response.statusText);
                }
            } catch (error) {
                console.error('Fetch error:', error);
                alert('Fetch error: ' + error.message);
            }
        }

        async function fetchAndUpdateChart() {
            try {
                const response = await fetch('/get_predictions');
                if (response.ok) {
                    const predictions = await response.json();
                    const labels = Object.keys(predictions);
                    const data = Object.values(predictions).map(arr => arr[0]);  // Take the first prediction if there are multiple
                    createChart(labels, data);
                } else {
                    console.error('Error fetching predictions:', response.statusText);
                }
            } catch (error) {
                console.error('Fetch error:', error);
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            const form = document.getElementById('energyForm');
            form.addEventListener('submit', handleFormSubmit);
        });