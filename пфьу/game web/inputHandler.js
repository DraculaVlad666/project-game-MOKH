class InputHandler {
    constructor() {
        this.keys = [];

        window.addEventListener('keydown', (e) => {
            if ((e.key === ' ' || e.key === 'Enter') && !this.keys.includes(e.key)) {
                this.keys.push(e.key);
            }
        });

        window.addEventListener('keyup', (e) => {
            this.keys = this.keys.filter(key => key !== e.key);
        });
    }
}