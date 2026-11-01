// Minimal discriminator for the H100 arm-B failure: does a CUDA-10.2 PTX (compute_75) module that uses
// dynamic parallelism with device-side cudaDeviceSynchronize (CDP1, as voxcraft-sim does) load on this GPU?
#include <cstdio>
#include <cuda_runtime.h>
__global__ void child(int *x) { x[threadIdx.x] = 1; }
__global__ void plain(int *x) { x[0] = 7; }
#ifdef WITH_CDP
__global__ void parent(int *x) { child<<<1, 32>>>(x); cudaDeviceSynchronize(); x[40] = 9; }
#endif
#define R(call) do { cudaError_t e = (call); printf("%-40s -> %d %s : %s\n", #call, (int)e, cudaGetErrorName(e), cudaGetErrorString(e)); } while (0)
int main() {
  int drv = 0, rt = 0; cudaDriverGetVersion(&drv); cudaRuntimeGetVersion(&rt);
  printf("driver_api_version=%d runtime_version=%d\n", drv, rt);
  int *d = 0; R(cudaMalloc(&d, 256 * sizeof(int)));
  plain<<<1, 1>>>(d); R(cudaGetLastError()); R(cudaDeviceSynchronize());
#ifdef WITH_CDP
  parent<<<1, 1>>>(d); R(cudaGetLastError()); R(cudaDeviceSynchronize());
  int h[64]; R(cudaMemcpy(h, d, sizeof(h), cudaMemcpyDeviceToHost)); printf("x[0]=%d x[1]=%d x[40]=%d\n", h[0], h[1], h[40]);
#endif
  return 0;
}
