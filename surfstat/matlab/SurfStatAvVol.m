function [ data, vol ] = SurfStatAvVol( filenames, fun, Nan, dimensionality);

%Average, minimum or maximum of MINC, ANALYZE, NIFTI or AFNI volumes.
%
% Usage: [ data, vol ] = SurfStatAvVol( filenames [, fun [, Nan ]]);
%
% filenames = file name with extension .mnc, .img, .nii or .brik as above 
%             (n=1), or n x 1 cell array of file names.
% fun       = function handle to apply to two volumes, e.g. 
%           = @plus (default) will give the average of the volumes,
%           = @min or @max will give the min or max, respectively.
% Nan       = value to replace NaN in data, default NaN.
%
% data       = nx x ny x nz array of average, min or max volume.
% vol.lat    = logical(ones(nx,ny,nz)) (this is needed for SurfStatView1).
% vol.vox    = 1 x 3 vector of voxel sizes in mm.
% vol.origin = position in mm of the first voxel.

if nargin<2 | isempty(fun)
    fun=@plus;
end
if nargin<3
    Nan=NaN;
end

if nargin<4
    dimensionality = size(filenames);
end
if isempty(dimensionality)
    dimensionality = size(filenames);
end

filenames = reshape(filenames, dimensionality);
n=size(filenames,1);

if n==1
    d=SurfStatReadVol1(filenames);
    data=d.data;
else
    fprintf(1,'%s',[num2str(n) ' files to read, % remaining: 100 ']);
    n10=floor(n/10);
    for i=1:n
        if rem(i,n10)==0 
            fprintf(1,'%s',[num2str(round(100*(1-i/n))) ' ']);
        end
        d=SurfStatReadVol1(filenames{i});

        %  niftiread for a proper *nii or *nii.gz data read-in
        if filenames{i}(end-3:end) == '.nii' 
            d.data = niftiread(filenames{i});
        end

        if ~isnan(Nan)
            % analyze75read for a proper NaN-value reading
            if filenames{i}(end-3:end) == '.img'
                d.data = analyze75read(filenames{i});
                % transposing 3D array to match with python analyze reader
                d.data = permute(d.data, [2,1,3]);
                d.data(isnan(d.data))=Nan;
            elseif filenames{i}(end-3:end) == '.nii' 
                d.data(isnan(d.data))
                d.data(isnan(d.data))=Nan;
            end
        end

        if i==1
            if filenames{i}(end-3:end) == '.img'
                data = d.data;
            elseif filenames{i}(end-3:end) == '.nii'
                data = niftiread(filenames{i});
            end
            m = 1;
        else
            data=fun(data,d.data);
            m=fun(m,1);
        end
    end
    fprintf(1,'%s\n','Done');
end
data=data/m;
vol.lat=logical(ones(d.dim(1:3)));
vol.vox=d.vox(1:3);
vol.origin=d.origin;

return
end
