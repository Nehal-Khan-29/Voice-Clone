const flashContainer = document.getElementById('flash-messages');
if (flashContainer) {
    setTimeout(() => {
        flashContainer.style.display = 'none';
    }, 3000);
}
