M.AutoInit();

function addQuantity(element, displayID) {
    const display = document.getElementById(displayID);
    display.classList.add('keep-display');
    display.value = display.value + element.value;
}

document.addEventListener('DOMContentLoaded', function () {
    const userSideNavElems = document.querySelectorAll('.sidenav.user-sidenav');
    const userSideNavInstances = M.Sidenav.init(userSideNavElems, {
        edge: 'right',
    });

    const materialTextBoxElems = document.querySelectorAll('.materialize-textbox');
    const materialTextBoxInstances = M.CharacterCounter.init(materialTextBoxElems);

    const materialFloatingButtonElems = document.querySelectorAll('.fixed-action-btn');
    const materialFloatingButtonInstances = M.FloatingActionButton.init(materialFloatingButtonElems, {
        hoverEnabled: false,
    });


    addQuantity();

});
