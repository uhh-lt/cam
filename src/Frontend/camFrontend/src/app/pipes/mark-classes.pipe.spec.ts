import { MarkClassesPipe } from './mark-classes.pipe';
import { DomSanitizer } from '@angular/platform-browser';

describe('MarkClassesPipe', () => {
  const pipe = MarkClassesPipe;

  it('create an instance', () => {
    expect(pipe).toBeTruthy();
  });
});
