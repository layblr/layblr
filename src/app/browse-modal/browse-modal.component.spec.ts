import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BrowseModalComponent } from './browse-modal.component';

describe('BrowseModalComponent', () => {
  let component: BrowseModalComponent;
  let fixture: ComponentFixture<BrowseModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BrowseModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BrowseModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
