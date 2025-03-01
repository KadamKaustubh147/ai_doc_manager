// pehle

document.body.addEventListener('htmx:afterSwap', function(event) {
      // Reinitialize Flowbite dropdowns
      if (typeof window.initFlowbite === 'function') {
          window.initFlowbite();
      }
});