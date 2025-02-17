document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileServicesButton = document.getElementById('mobileServicesButton');
    const mobileToolsButton = document.getElementById('mobileToolsButton');
    const mobileProgramsButton = document.getElementById('mobileProgramsButton');
    const mobileBlogButton = document.getElementById('mobileBlogButton');
    const mobileServicesMenu = document.getElementById('mobileServicesMenu');
    const mobileToolsMenu = document.getElementById('mobileToolsMenu');
    const mobileProgramsMenu = document.getElementById('mobileProgramsMenu');
    const mobileBlogMenu = document.getElementById('mobileBlogMenu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Services dropdown toggle
    if (mobileServicesButton && mobileServicesMenu) {
        mobileServicesButton.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileServicesMenu.classList.toggle('hidden');
            this.querySelector('svg:last-child').classList.toggle('rotate-180');
            // Close other menus
            if (mobileToolsMenu && !mobileToolsMenu.classList.contains('hidden')) {
                mobileToolsMenu.classList.add('hidden');
                mobileToolsButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileProgramsMenu && !mobileProgramsMenu.classList.contains('hidden')) {
                mobileProgramsMenu.classList.add('hidden');
                mobileProgramsButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileBlogMenu && !mobileBlogMenu.classList.contains('hidden')) {
                mobileBlogMenu.classList.add('hidden');
                mobileBlogButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
        });
    }

    // Tools dropdown toggle
    if (mobileToolsButton && mobileToolsMenu) {
        mobileToolsButton.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileToolsMenu.classList.toggle('hidden');
            this.querySelector('svg:last-child').classList.toggle('rotate-180');
            // Close other menus
            if (mobileServicesMenu && !mobileServicesMenu.classList.contains('hidden')) {
                mobileServicesMenu.classList.add('hidden');
                mobileServicesButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileProgramsMenu && !mobileProgramsMenu.classList.contains('hidden')) {
                mobileProgramsMenu.classList.add('hidden');
                mobileProgramsButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileBlogMenu && !mobileBlogMenu.classList.contains('hidden')) {
                mobileBlogMenu.classList.add('hidden');
                mobileBlogButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
        });
    }

    // Programs dropdown toggle
    if (mobileProgramsButton && mobileProgramsMenu) {
        mobileProgramsButton.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileProgramsMenu.classList.toggle('hidden');
            this.querySelector('svg:last-child').classList.toggle('rotate-180');
            // Close other menus
            if (mobileServicesMenu && !mobileServicesMenu.classList.contains('hidden')) {
                mobileServicesMenu.classList.add('hidden');
                mobileServicesButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileToolsMenu && !mobileToolsMenu.classList.contains('hidden')) {
                mobileToolsMenu.classList.add('hidden');
                mobileToolsButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileBlogMenu && !mobileBlogMenu.classList.contains('hidden')) {
                mobileBlogMenu.classList.add('hidden');
                mobileBlogButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
        });
    }

    // Blog dropdown toggle
    if (mobileBlogButton && mobileBlogMenu) {
        mobileBlogButton.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileBlogMenu.classList.toggle('hidden');
            this.querySelector('svg:last-child').classList.toggle('rotate-180');
            // Close other menus
            if (mobileServicesMenu && !mobileServicesMenu.classList.contains('hidden')) {
                mobileServicesMenu.classList.add('hidden');
                mobileServicesButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileToolsMenu && !mobileToolsMenu.classList.contains('hidden')) {
                mobileToolsMenu.classList.add('hidden');
                mobileToolsButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileProgramsMenu && !mobileProgramsMenu.classList.contains('hidden')) {
                mobileProgramsMenu.classList.add('hidden');
                mobileProgramsButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (mobileMenu && !mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
            mobileMenu.classList.add('hidden');
            // Reset all dropdowns when closing menu
            if (mobileServicesMenu) {
                mobileServicesMenu.classList.add('hidden');
                mobileServicesButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileToolsMenu) {
                mobileToolsMenu.classList.add('hidden');
                mobileToolsButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileProgramsMenu) {
                mobileProgramsMenu.classList.add('hidden');
                mobileProgramsButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
            if (mobileBlogMenu) {
                mobileBlogMenu.classList.add('hidden');
                mobileBlogButton.querySelector('svg:last-child').classList.remove('rotate-180');
            }
        }
    });

    // Prevent menu close when clicking inside dropdowns
    mobileMenu.addEventListener('click', function(e) {
        e.stopPropagation();
    });
}); 