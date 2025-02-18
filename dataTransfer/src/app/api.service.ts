import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {

  constructor(private http: HttpClient) {}

  getTables(type:string) {
    return this.http.get('http://localhost:5000/tables', { params: {type} } );
  }

  transferData(tables: string[], updateTwoRows: boolean): Observable<any> {
    return this.http.post('http://localhost:5000/transfer1', {
      tables: tables,
      ...(updateTwoRows && {
        limit_rows: 2,
      }),
    });
  }
}
