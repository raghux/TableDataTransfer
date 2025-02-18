import { Component } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

// services
import { ApiService } from './api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'dataTransfer';

  sourceTables: string[] = [];
  destTables: string[] = [];
  selectedTables: string[] = [];
  status: string = '';
  updateTwoRows: boolean = false;

  private onDestroy = new Subject<void>()

  constructor(private apiService: ApiService) {}

  ngOnDestroy(){
   this.onDestroy.next()
   this.onDestroy.complete()
  }

  ngOnInit(): void {
    this.fetchTables();
  }

  fetchTables(): void {
    this.apiService.getTables('source')
    .pipe(takeUntil(this.onDestroy))
    .subscribe((data: any) => {
      this.sourceTables = data?.tables as unknown as string[];
    });

    this.apiService.getTables('dest')
    .pipe(takeUntil(this.onDestroy))
    .subscribe((data: any) => {
      this.destTables = data?.tables as unknown as string[];
    });
  }

  onTableSelection(event: any): void {
    const value = event.target.value;
    if (event.target.checked) {
      this.selectedTables.push(value);
    } else {
      this.selectedTables = this.selectedTables.filter(
        (table) => table !== value
      );
    }
  }

  transferData(): void {
    if (this.selectedTables.length === 0) {
      this.status = 'No tables selected!';
      return;
    }
    this.apiService
      .transferData(this.selectedTables, this.updateTwoRows)
      .pipe(takeUntil(this.onDestroy))
      .subscribe((response: any) => {
        this.status = Object.values(response)[0] as string;
        this.refreshDbTables()       
      });
  }
  
  refreshDbTables(){
    this.apiService.getTables('source')
    this.apiService.getTables('dest')
  }
}
