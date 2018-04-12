export class Result {

    constructor() {
        this.objectA = '';
        this.objectB = '';
        this.winnerAspects = new Array<string>();
        this.looserAspects = new Array<string>();
        this.sentencesObjectA = new Array<string>();
        this.sentencesObjectB = new Array<string>();
        this.winnerScorePercent = '';
        this.looserScorePercent = '';
        this.winner = '';
        this.looser = '';
    }

    objectA: string;
    objectB: string;
    winnerAspects: Array<string>; // stores the main links of the first object
    looserAspects: Array<string>; // stores the main links of the second object
    sentencesObjectA: Array<string>;
    sentencesObjectB: Array<string>;
    winnerScorePercent: string; // stores the score of the first object
    looserScorePercent: string; // stores the score of the second object
    winner: string; // the winning object of the results shown
    looser: string; // the losing object of the results shown
}
