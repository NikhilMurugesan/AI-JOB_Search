import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';

import { JobCard } from '../../core/models/job.model';
import { JobsApiService } from '../../core/services/jobs-api.service';

@Component({
  selector: 'app-dashboard-page',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.scss'
})
export class DashboardPageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly jobsApi = inject(JobsApiService);

  readonly filterForm = this.fb.group({
    role: [''],
    company: [''],
    location: [''],
    status: [''],
    source: ['']
  });

  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly jobs = signal<JobCard[]>([]);

  readonly summary = computed(() => ({
    total: this.jobs().length,
    readyOrApplied: this.jobs().filter((job) => ['READY', 'APPLIED'].includes(job.status)).length
  }));

  constructor() {
    this.loadJobs();
  }

  loadJobs(): void {
    this.loading.set(true);
    this.error.set(null);

    const value = this.filterForm.getRawValue();

    this.jobsApi.listJobs(value).subscribe({
      next: (jobs) => {
        this.jobs.set(jobs);
        this.loading.set(false);
      },
      error: () => {
        this.jobs.set(this.fallbackJobs());
        this.error.set('Backend unavailable. Showing fallback demo data for portfolio preview.');
        this.loading.set(false);
      }
    });
  }

  private fallbackJobs(): JobCard[] {
    return [
      {
        id: 'job-1',
        company: 'OpenSource Labs',
        role: 'LLM Engineer',
        location: 'Remote (US)',
        source: 'Remotive',
        dateFound: new Date().toISOString().slice(0, 10),
        relevanceScore: 91,
        status: 'READY'
      },
      {
        id: 'job-2',
        company: 'DataOrbit',
        role: 'AI Engineer',
        location: 'New York, NY',
        source: 'Public API',
        dateFound: new Date().toISOString().slice(0, 10),
        relevanceScore: 84,
        status: 'SAVED'
      }
    ];
  }
}
