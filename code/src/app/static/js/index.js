document.addEventListener('DOMContentLoaded', function () {

    // GET DATA SOURCES
    const DataSourceOne = document.getElementById('data-source-one');
    const DataSourceTwo = document.getElementById('data-source-two');
    const submitDataSource = document.getElementById('submitDataSource');

    // GET INPUT FIELDS
    const KeyColumns = document.getElementById('key-columns');
    const CriteriaColumns = document.getElementById('criteria-columns');
    const DerivedColumns = document.getElementById('derived-columns');
    const HistoricalColumns = document.getElementById('historical-columns');
    const DateColumns = document.getElementById('date-columns');


    function update_datasource(Field, Data) {

        Field.innerHTML = '<option value="">Select source</option>';

        // Populate with new options
        Data.data_sources.forEach(item => {
            const option = document.createElement('option');
            option.value = item.value; // Assuming each object has a `value` field
            option.textContent = item.label; // Assuming each object has a `label` field
            Field.appendChild(option);
        });
    }

    function update_input_fields(Field, Data) {

        // Populate with new options
        Data.COLUMNS.forEach(item => {
            const option = document.createElement('option');
            option.value = item.value; // Assuming each object has a `value` field
            option.textContent = item.label; // Assuming each object has a `label` field
            Field.appendChild(option);
        });

    }

    async function updateInputFieldsOptions(DataSourceOne, DataSourceTwo) {

        let RequestBody = {
            'DataSourceOne': DataSourceOne,
            'DataSourceTwo': DataSourceTwo
        };

        const response = await fetch('/getDataSourceColumnsList', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(RequestBody)
        });

        if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON data
        const columns = await response.json(); // Assuming the response is an array of objects

        update_input_fields(KeyColumns, columns);
        update_input_fields(CriteriaColumns, columns);
        update_input_fields(DerivedColumns, columns);
        update_input_fields(HistoricalColumns, columns);
        update_input_fields(DateColumns, columns);

    }

    // Fetch data from the endpoint and populate the select element
    const updateDataSourceOptions = async () => {
        try {

            let requestBody = {
            };

            const response = await fetch('/getDataSources', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Parse the JSON data
            const dataSources = await response.json(); // Assuming the response is an array of objects

            // Update DataSource One
            update_datasource(DataSourceOne, dataSources);

            // Update DataSource Two
            update_datasource(DataSourceTwo, dataSources);

        } catch (error) {
            console.error('Error fetching data sources:', error);
        }
    };

    updateDataSourceOptions();

    function DisableDataSources() {
        DataSourceOne.disabled = true;
        DataSourceTwo.disabled = true;
    }

    function EnableDataSources() {
        DataSourceOne.disabled = false;
        DataSourceTwo.disabled = false;
    }

    function DisableInputFields() {
        KeyColumns.disabled = true;
        CriteriaColumns.disabled = true;
        DerivedColumns.disabled = true;
        HistoricalColumns.disabled = true;
        DateColumns.disabled = true;
    }

    function EnableInputFields() {
        KeyColumns.disabled = false;
        CriteriaColumns.disabled = false;
        DerivedColumns.disabled = false;
        HistoricalColumns.disabled = false;
        DateColumns.disabled = false;
    }

    submitDataSource.addEventListener('click', function() {

        // VALIDATE IF DataSourceOne AND DataSourceTwo ARE SELECTED
        if (DataSourceOne.value === '' || DataSourceTwo.value === '') {
            alert('Please select both data sources.');
            return;
        }

        if (DataSourceOne.value === DataSourceTwo.value) {
            alert('Cannot select same data sources.');
            return;
        }

        // DISABLE DATA SOURCES
        DisableDataSources();

        // ENABLE INPUT FIELDS
        EnableInputFields();

        // UPDATE THE INPUT FIELD COLUMNS
        updateInputFieldsOptions(DataSourceOne.value, DataSourceTwo.value);

    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Run Reconciliation button animation
    const runBtn = document.getElementById('runReconciliation');
    if (runBtn) {
        runBtn.addEventListener('click', function() {
            this.classList.add('pulse');
            setTimeout(() => {
                this.classList.remove('pulse');
            }, 2000);

            // Simulate processing
            setTimeout(() => {
                alert('Reconciliation completed successfully!');
            }, 3000);
        });
    }

    // Feedback button in table
    document.querySelectorAll('table .btn-outline').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = this.closest('tr');
            const id = row.querySelector('td:first-child').textContent;
            const anomaly = row.querySelector('.anomaly-type').textContent;
            alert(`Feedback dialog for ${anomaly} (${id}) would open here.`);
        });
    });
});