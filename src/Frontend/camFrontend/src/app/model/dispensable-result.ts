import { Sentence } from './sentence';

export class DispensableResult {

    constructor() {
        this.winnerLinks = new Array<string>();
        this.looserLinks = new Array<string>();
        this.winnerSentences = new Array<Sentence>();
        this.looserSentences = new Array<Sentence>();
        this.winnerScoresPercent = {};
        this.looserScoresPercent = {};
        this.winner = '';
        this.looser = '';
        this.winnerTotalScore = '';
        this.looserTotalScore = '';
    }

    winnerLinks: Array<string>; // stores the main links of the first object
    looserLinks: Array<string>; // stores the main links of the second object
    winnerSentences: Array<Sentence>;
    looserSentences: Array<Sentence>;
    winnerScoresPercent: {}; // stores the score of the first object
    looserScoresPercent: {}; // stores the score of the second object
    winner: string; // the winning object of the results shown
    looser: string; // the losing object of the results shown
    winnerTotalScore: string;
    looserTotalScore: string;
}
