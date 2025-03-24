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