// Simple test setup (you can use Jest, Mocha, or similar)
describe('ResponsiveNavigation', () => {
    let nav;
    
    beforeEach(() => {
        // Setup DOM
        document.body.innerHTML = `
            <nav class="nav">
                <button class="nav__toggle" aria-expanded="false"></button>
                <ul class="nav__menu">
                    <li><a href="#" class="nav__link">Home</a></li>
                    <li><a href="#" class="nav__link">About</a></li>
                </ul>
            </nav>
        `;
        
        nav = new ResponsiveNavigation();
    });
    
    test('should initialize without errors', () => {
        expect(nav).toBeDefined();
        expect(nav.isOpen).toBe(false);
    });
    
    test('should open menu when toggle is clicked', () => {
        const toggle = document.querySelector('.nav__toggle');
        const menu = document.querySelector('.nav__menu');
        
        toggle.click();
        
        expect(nav.isOpen).toBe(true);
        expect(menu.classList.contains('nav__menu--open')).toBe(true);
        expect(toggle.getAttribute('aria-expanded')).toBe('true');
    });
    
    test('should close menu when escape key is pressed', () => {
        // Open menu first
        nav.openMenu();
        expect(nav.isOpen).toBe(true);
        
        // Press escape
        const escapeEvent = new KeyboardEvent('keydown', { key: 'Escape' });
        document.dispatchEvent(escapeEvent);
        
        expect(nav.isOpen).toBe(false);
    });
    
    test('should close menu when clicking outside', () => {
        nav.openMenu();
        expect(nav.isOpen).toBe(true);
        
        // Click outside nav
        document.body.click();
        
        expect(nav.isOpen).toBe(false);
    });
});