export type ApplicationStatus =
  | 'SAVED'
  | 'TAILORED'
  | 'READY'
  | 'APPLIED'
  | 'INTERVIEW'
  | 'REJECTED'
  | 'OFFER';

export interface JobCard {
  id: string;
  company: string;
  role: string;
  location: string;
  source: string;
  dateFound: string;
  relevanceScore: number;
  status: ApplicationStatus;
}
