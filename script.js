class MobileNavigation {
    constructor() {
        this.navToggle = document.querySelector('.nav__toggle');
        this.navMenu = document.querySelector('.nav__menu');
        this.navLinks = document.querySelectorAll('.nav__link');
        
        this.init();
    }
    
    init() {
        if (!this.navToggle || !this.navMenu) {
            console.warn('Navigation elements not found');
            return;
        }
        
        this.bindEvents();
    }
    
    bindEvents() {
        // Toggle menu on button click
        this.navToggle.addEventListener('click', () => this.toggleMenu());
        
        // Close menu when clicking on links
        this.navLinks.forEach(link => {
            link.addEventListener('click', () => this.closeMenu());
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isMenuOpen()) {
                this.closeMenu();
            }
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.navToggle.contains(e.target) && !this.navMenu.contains(e.target)) {
                this.closeMenu();
            }
        });
    }
    
    toggleMenu() {
        const isOpen = this.isMenuOpen();
        
        if (isOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }
    
    openMenu() {
        this.navMenu.classList.add('nav__menu--open');
        this.navToggle.classList.add('nav__toggle--active');
        this.navToggle.setAttribute('aria-expanded', 'true');
        
        // Focus first menu item for accessibility
        const firstLink = this.navMenu.querySelector('.nav__link');
        if (firstLink) {
            firstLink.focus();
        }
    }
    
    closeMenu() {
        this.navMenu.classList.remove('nav__menu--open');
        this.navToggle.classList.remove('nav__toggle--active');
        this.navToggle.setAttribute('aria-expanded', 'false');
    }
    
    isMenuOpen() {
        return this.navMenu.classList.contains('nav__menu--open');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MobileNavigation();
});