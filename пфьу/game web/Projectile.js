class Projectile {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.speed = 5;
        this.size = 10;
    }

    update() {
        this.y -= this.speed;
    }

    draw(ctx) {
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}