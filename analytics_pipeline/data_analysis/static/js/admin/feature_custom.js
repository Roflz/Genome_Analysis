// static/js/admin/feature_custom.js
document.addEventListener('DOMContentLoaded', function() {
    const tooltips = document.querySelectorAll('.feature-tooltip');
    tooltips.forEach(function(tooltip) {
        tooltip.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#ffeb3b';
        });
        tooltip.addEventListener('mouseout', function() {
            this.style.backgroundColor = '';
        });
    });
});
