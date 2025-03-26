document.addEventListener('DOMContentLoaded', function () {

    // GET DATA SOURCES
    const DataSourceOne = document.getElementById('data-source-one');
    const DataSourceTwo = document.getElementById('data-source-two');
    const submitDataSource = document.getElementById('submitDataSource');

    // GET INPUT FIELDS
    const KeyColumns = document.getElementById('key-columns');
    const CriteriaColumns = document.getElementById('criteria-columns');
    const DateColumns = document.getElementById('date-columns');
    const RunRecon = document.getElementById('runReconciliation');

    // Reporting Summary Counts
    const SummaryCardSuccessCount = document.getElementById('TotalSuccessCount');
    const SummaryCardPotentialIssuesCount = document.getElementById('PotentialIssuesCount');
    const SummaryCardCriticalAnomaliesCount = document.getElementById('CriticalAnomaliesCount');
    const SummaryCardLastRunTimeStamp = document.getElementById('LastRunTimeStamp');

    // Reporting Data
    const AnomalyTable = document.getElementById('AnomaliesDetectedTable');
    const AIInsights = document.getElementById('AIGeneratedInsights');
    const AITrendSummary = document.getElementById('AITrendSummary');

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
            const dataSources = await response.json();

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
        DateColumns.disabled = true;
    }

    function EnableInputFields() {
        KeyColumns.disabled = false;
        CriteriaColumns.disabled = false;
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

    async function update_ai_insights(aiInsights) {

        let htmlOutput = '';

        // Loop through the AIInsights array to build the HTML string
        aiInsights.forEach(insight => {
            if (insight !== "") { // Skip empty strings
                htmlOutput += `${insight}<br>`;
            } else {
                htmlOutput += `<br>`; // Add an extra line break for empty strings
            }
        });

        AIInsights.innerHTML = htmlOutput;

    }

    async function update_anomalies_table(content) {
        AnomalyTable.innerHTML = content;
    }

    async function update_ai_trend_summary(content) {
        AITrendSummary.textContent = content;
    }

    async function update_summary_cards(TotalSuccessCount, PotentialIssuesCount, CriticalAnomaliesCount) {

        // Get the current date and time
        const now = new Date();
        const formattedTimestamp = now.toLocaleString(); // Format as a readable string

        SummaryCardSuccessCount.textContent = TotalSuccessCount;
        SummaryCardPotentialIssuesCount.textContent = PotentialIssuesCount;
        SummaryCardCriticalAnomaliesCount.textContent = CriticalAnomaliesCount;
        SummaryCardLastRunTimeStamp.textContent = `Last run: ${formattedTimestamp}`;

    }

    function get_selected_values(current_form) {
        const selectedValues = Array.from(current_form.selectedOptions).map(option => option.label);
        return selectedValues;
    }

    RunRecon.addEventListener('click', async function() {

        // Key Columns Selected & Validation
        const keyColumnSel = get_selected_values(KeyColumns);

        if ( keyColumnSel.length === 0 || keyColumnSel.some(value => value === "") ) {
            alert('Please select appropriate Key Columns.');
            return;
        }

        // Criteria Columns Selected & Validation
        const CriteriaColumnSel = get_selected_values(CriteriaColumns);

        if ( CriteriaColumnSel.length === 0 || CriteriaColumnSel.some(value => value === "") ) {
            alert('Please select appropriate Criteria Columns.');
            return;
        }


        // Date Columns Selection & Validation
        const DateColumnSel = get_selected_values(DateColumns);

        if ( DateColumnSel.length === 0 || DateColumnSel.some(value => value === "") ) {
            alert('Please select appropriate Date Columns.');
            return;
        }


        let RequestBody = {
            "KeyColumns": keyColumnSel,
            "CriteriaColumns": CriteriaColumnSel,
            "DateColumns": DateColumnSel
        }


        const response = await fetch('/RunReconcile', {
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
        const data = await response.json();

        // Update Summary Cards Section
        await update_summary_cards(
            data.summary.success,
            data.summary.PotentialIssue,
            data.summary.CriticalIssue
        );

        // Update AI Insights
        await update_ai_insights(data.Details.AIInsights);

        // Update Anomalies Table
        await update_anomalies_table(data.Details.AnomaliesDetectedTable);

        // Update AI Trend Analysis Summary
        await update_ai_trend_summary(data.Details.AITrendAnalysisSummary);

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