import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  template: `
    <main class="container">
      <h1>AI Job Search Copilot</h1>
      <p class="subtitle">Step 1 UI foundation: dashboard shell + API integration seam.</p>
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [
    `
      .subtitle {
        margin-top: -0.5rem;
        color: #4a5b75;
      }
    `
  ]
})
export class AppComponent {}
