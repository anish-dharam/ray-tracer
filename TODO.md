# TODOs

- [x] change vec3 to use fields instead of methods to get x, y, z (10-15% speedup)
- [x] remove front_face field from hittables (0.004% speedup) (undone because used in dielectrics)
- [x] try inlining random_float, see performance
- [ ] change Optional annotations to \_ | None
- [ ] get rid of HitRecords, just pass around HitRecord arguments (sacrifice readability for performance)
