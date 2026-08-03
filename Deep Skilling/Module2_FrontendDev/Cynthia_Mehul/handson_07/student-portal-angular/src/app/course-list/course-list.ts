import { Component, OnInit, ChangeDetectorRef  } from '@angular/core';
import {CommonModule} from '@angular/common';
import {CourseCard} from  '../course-card/course-card';
import { FormsModule } from '@angular/forms';
import { Course } from '../course';

@Component({
  selector: 'app-course-list',
  imports: [CommonModule, FormsModule, CourseCard],
  templateUrl: './course-list.html',
  styleUrl: './course-list.css',
})
export class CourseList implements OnInit{
  constructor(private courseService: Course, private cdr: ChangeDetectorRef) {}
  searchTerm='';
  loading=true;
  courses: any[] = [];

  ngOnInit(): void {
  this.courseService.getCourses().subscribe((data) => {
    this.courses = data.map((post) => ({
        name: post.title,
        code: `CS${post.id}`, 
        credits: 3,
        grade: 'A'
      }));
      this.loading=false;
      this.cdr.detectChanges();
    });
  }

  get filteredCourses() {
  return this.courses.filter((course) =>
    course.name.toLowerCase().includes(
      this.searchTerm.toLowerCase()
    )
  );
}
}
