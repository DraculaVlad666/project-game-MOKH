class Player {
    constructor() {
        this.score = 0;
        this.level = 1;
    }

    increaseScore(points) {
        this.score += points;
    }

    nextLevel() {
        this.level++;
    }

    reset() {
        this.score = 0;
        this.level = 1;
    }
}