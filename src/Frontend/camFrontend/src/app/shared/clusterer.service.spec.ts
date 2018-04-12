import { TestBed, inject } from '@angular/core/testing';

import { ClustererService } from './clusterer.service';

describe('ClustererService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ClustererService]
    });
  });

  it('should be created', inject([ClustererService], (service: ClustererService) => {
    expect(service).toBeTruthy();
  }));
});
