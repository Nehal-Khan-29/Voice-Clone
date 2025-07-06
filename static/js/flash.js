const flashContainer = document.getElementById('flash-messages');
if (flashContainer) {
    setTimeout(() => {
        flashContainer.style.opacity = '0';
        setTimeout(() => {
            flashContainer.style.display = 'none';
        }, 500);
    }, 3000);
}
