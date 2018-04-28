import { HAMMER_GESTURE_CONFIG  } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MatProgressSpinnerModule,
  MatInputModule,
  MatSliderModule,
  MatCardModule,
  MatButtonModule,
  GestureConfig,
  MatIconModule,
  MatSelectModule,
  MatCheckboxModule,
  MatToolbarModule,
  MatDividerModule,
  MatSnackBarModule,
  MatMenuModule
} from '@angular/material';

@NgModule({
  exports: [
    MatProgressSpinnerModule,
    MatInputModule,
    MatSliderModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatSelectModule,
    MatCheckboxModule,
    MatToolbarModule,
    MatDividerModule,
    MatSnackBarModule,
    MatMenuModule
  ],
  providers: [{provide: HAMMER_GESTURE_CONFIG, useClass: GestureConfig}]
})
export class MaterialModule {}
