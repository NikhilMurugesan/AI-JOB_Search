import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { JobCard } from '../models/job.model';

@Injectable({ providedIn: 'root' })
export class JobsApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = 'http://127.0.0.1:8000/api/v1';

  listJobs(filters?: Partial<Pick<JobCard, 'role' | 'company' | 'location' | 'source' | 'status'>>): Observable<JobCard[]> {
    let params = new HttpParams();

    Object.entries(filters ?? {}).forEach(([key, value]) => {
      if (value) {
        params = params.set(key, value);
      }
    });

    return this.http.get<JobCard[]>(`${this.baseUrl}/jobs`, { params });
  }
}
