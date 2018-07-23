export class DispensableResult {

    constructor() {
        this.winnerLinks = new Array<string>();
        this.looserLinks = new Array<string>();
        this.winnerSentences = new Array<string>();
        this.looserSentences = new Array<string>();
        this.winnerScoresPercent = {};
        this.looserScoresPercent = {};
        this.winner = '';
        this.looser = '';
        this.winnerTotalScore = '';
        this.looserTotalScore = '';
        this.winnerSources = new Array<string>();
        this.looserSources = new Array<string>();
    }

    winnerLinks: Array<string>; // stores the main links of the first object
    looserLinks: Array<string>; // stores the main links of the second object
    winnerSentences: Array<string>;
    looserSentences: Array<string>;
    winnerScoresPercent: {}; // stores the score of the first object
    looserScoresPercent: {}; // stores the score of the second object
    winner: string; // the winning object of the results shown
    looser: string; // the losing object of the results shown
    winnerTotalScore: string;
    looserTotalScore: string;
    winnerSources: Array<string>;
    looserSources: Array<string>;
}
