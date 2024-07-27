//------------- API FETCH CHEYYANAM KURACH KAZHINJ -------------
//------------- WILL BE UPDATED IN FUTURE ----------------------

const metrics = {
    totalTests: 4,
    passedTests: 2,
    failedTests: 2,
    successRate: 50.00
};

function updateMetrics() {
    document.getElementById('total-tests').innerText = metrics.totalTests;
    document.getElementById('passed-tests').innerText = metrics.passedTests;
    document.getElementById('failed-tests').innerText = metrics.failedTests;
    document.getElementById('success-rate').innerText = `${metrics.successRate}%`;
}

document.addEventListener('DOMContentLoaded', updateMetrics);
