class MobileNavigation {
    constructor() {
        this.toggle = document.querySelector('.nav__toggle');
        this.menu = document.querySelector('.nav__menu');
        this.links = document.querySelectorAll('.nav__link');
        
        this.init();
    }
    
    init() {
        if (!this.toggle || !this.menu) {
            console.warn('Navigation elements not found');
            return;
        }
        
        this.toggle.addEventListener('click', () => this.toggleMenu());
        this.links.forEach(link => {
            link.addEventListener('click', () => this.closeMenu());
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isMenuOpen()) {
                this.closeMenu();
            }
        });
        
        // Close menu on outside click
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.nav') && this.isMenuOpen()) {
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
        this.menu.classList.add('nav__menu--open');
        this.toggle.setAttribute('aria-expanded', 'true');
    }
    
    closeMenu() {
        this.menu.classList.remove('nav__menu--open');
        this.toggle.setAttribute('aria-expanded', 'false');
    }
    
    isMenuOpen() {
        return this.menu.classList.contains('nav__menu--open');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MobileNavigation();
});