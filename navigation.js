class ResponsiveNavigation {
    constructor() {
        this.nav = document.querySelector('.nav');
        this.toggle = document.querySelector('.nav__toggle');
        this.menu = document.querySelector('.nav__menu');
        this.menuLinks = document.querySelectorAll('.nav__link');
        this.body = document.body;
        
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        if (!this.toggle || !this.menu) {
            console.warn('Navigation elements not found');
            return;
        }
        
        this.bindEvents();
    }
    
    bindEvents() {
        // Toggle button click
        this.toggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleMenu();
        });
        
        // Close menu when clicking on links (mobile)
        this.menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (this.isOpen) {
                    this.closeMenu();
                }
            });
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeMenu();
                this.toggle.focus();
            }
        });
        
        // Close menu on outside click
        document.addEventListener('click', (e) => {
            if (this.isOpen && !this.nav.contains(e.target)) {
                this.closeMenu();
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768 && this.isOpen) {
                this.closeMenu();
            }
        });
    }
    
    toggleMenu() {
        if (this.isOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }
    
    openMenu() {
        this.isOpen = true;
        this.menu.classList.add('nav__menu--open');
        this.toggle.classList.add('nav__toggle--open');
        this.toggle.setAttribute('aria-expanded', 'true');
        this.body.classList.add('body--menu-open');
        
        // Focus first menu item for accessibility
        const firstLink = this.menu.querySelector('.nav__link');
        if (firstLink) {
            firstLink.focus();
        }
    }
    
    closeMenu() {
        this.isOpen = false;
        this.menu.classList.remove('nav__menu--open');
        this.toggle.classList.remove('nav__toggle--open');
        this.toggle.setAttribute('aria-expanded', 'false');
        this.body.classList.remove('body--menu-open');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ResponsiveNavigation();
});