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

        /* Author: Ali
        Changes: introduced new variables to be used in score-presentation.component for in-order presentation of objects
        */  
        this.obj1 = '';
        this.obj2 = '';
        this.LinksObj1 = new Array<string>();
        this.LinksObj2 = new Array<string>();
        this.winnerSentencesObj1 = new Array<Sentence>();
        this.looserSentencesObj2 = new Array<Sentence>();
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

    // Author: Ali
    obj1: string;
    obj2: string;
    LinksObj1: Array<string>;
    LinksObj2: Array<string>;
    winnerSentencesObj1: Array<Sentence>;
    looserSentencesObj2: Array<Sentence>;
}

