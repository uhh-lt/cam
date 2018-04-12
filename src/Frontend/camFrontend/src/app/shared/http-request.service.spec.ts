import { TestBed, inject } from '@angular/core/testing';

import { HTTPRequestService } from './http-request.service';

describe('HTTPRequestService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [HTTPRequestService]
    });
  });

  it('should be created', inject([HTTPRequestService], (service: HTTPRequestService) => {
    expect(service).toBeTruthy();
  }));
});
