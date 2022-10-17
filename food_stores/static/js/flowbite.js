const targetEl = document.getElementById('registerSuccess');

const options = {
  triggerEl: document.getElementById('registerClose'),
  transition: 'transition-opacity',
  duration: 1000,
  timing: 'ease-out',

  onHide: (context, targetEl) => {
    console.log('element has been dismissed')
    console.log(targetEl)
  }
};

const dismiss = new Dismiss(targetEl, options);
dismiss.hide();