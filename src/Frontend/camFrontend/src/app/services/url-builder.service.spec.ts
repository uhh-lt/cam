import { TestBed, inject } from '@angular/core/testing';

import { UrlBuilderService } from './url-builder.service';

describe('UrlBuilderService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [UrlBuilderService]
    });
  });

  it('should be created', inject([UrlBuilderService], (service: UrlBuilderService) => {
    expect(service).toBeTruthy();
  }));
});
