import { TestBed, inject } from '@angular/core/testing';

import { CcrUrlBuilderService } from './ccr-url-builder.service';

describe('CcrUrlBuilderService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CcrUrlBuilderService]
    });
  });

  it('should be created', inject([CcrUrlBuilderService], (service: CcrUrlBuilderService) => {
    expect(service).toBeTruthy();
  }));
});
