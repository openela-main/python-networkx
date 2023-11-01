%global srcname networkx

Name:           python-%{srcname}
Version:        2.6.2
Release:        2%{?dist}
Summary:        Creates and Manipulates Graphs and Networks
License:        BSD
URL:            http://networkx.github.io/
Source0:        https://github.com/networkx/networkx/archive/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}

%if 0%{?rhel} == 0
BuildRequires:  python3-docs
BuildRequires:  %{py3_dist gdal}
BuildRequires:  %{py3_dist lxml}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist nb2plots}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist numpydoc}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist pillow}
BuildRequires:  %{py3_dist pydot}
BuildRequires:  %{py3_dist pygraphviz}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-cov}
BuildRequires:  %{py3_dist pyyaml}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-gallery}
BuildRequires:  %{py3_dist sphinx-rtd-theme}
BuildRequires:  %{py3_dist texext}
BuildRequires:  xdg-utils

# Documentation
BuildRequires:  tex(latex)
BuildRequires:  tex-preview
%endif

%description
NetworkX is a Python package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%package -n python3-%{srcname}
Summary:        Creates and Manipulates Graphs and Networks
Recommends:     %{py3_dist gdal}
Recommends:     %{py3_dist lxml}
Recommends:     %{py3_dist matplotlib}
Recommends:     %{py3_dist numpy}
Recommends:     %{py3_dist pandas}
Recommends:     %{py3_dist pillow}
Recommends:     %{py3_dist pydot}
Recommends:     %{py3_dist pygraphviz}
Recommends:     %{py3_dist pyparsing}
Recommends:     %{py3_dist pyyaml}
Recommends:     %{py3_dist scipy}
Recommends:     xdg-utils

# This can be removed when Fedora 30 reaches EOL
Obsoletes:      python3-%{srcname}-test < 2.3-2
Provides:       python3-%{srcname}-test = %{version}-%{release}

%description -n python3-%{srcname}
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%if 0%{?rhel} == 0
%package doc
Summary:        Documentation for networkx
Requires:       font(fontawesome)
Requires:       font(lato)
Requires:       font(robotoslab)
Provides:       bundled(jquery)
Provides:       bundled(js-underscore)

%description doc
Documentation for networkx
%endif

%prep
%autosetup -p0 -n %{srcname}-%{srcname}-%{version}

# Do not use env
for f in $(grep -FRl %{_bindir}/env .); do
  sed -e 's,%{_bindir}/env python[[:digit:]]*,%{python3},' \
      -e 's,%{_bindir}/env ,%{_bindir},' \
      -i.orig $f
  touch -r $f.orig $f
  rm $f.orig
done

# Use local objects.inv for intersphinx
sed -e 's|\("https://docs\.python\.org/3/": \)None|\1"%{_docdir}/python3-docs/html/objects.inv"|' \
    -e 's|\("https://numpy\.org/doc/stable/": \)None|\1"%{_docdir}/python3-numpy-doc/objects.inv"|' \
    -i doc/conf.py

%build
%py3_build

%if 0%{?rhel} == 0
# Build the documentation
PYTHONPATH=$PWD/build/lib make -C doc html
rst2html --no-datestamp README.rst README.html
%endif

%install
%py3_install
mv %{buildroot}%{_docdir}/networkx-%{version} ./installed-docs
rm -f installed-docs/INSTALL.txt

%if 0%{?rhel} == 0
# Repack uncompressed zip archives
for fil in $(find doc/build -name \*.zip); do
  mkdir zip
  cd zip
  unzip ../$fil
  zip -9r ../$fil .
  cd ..
  rm -fr zip
done
%endif

%check
%if 0%{?rhel} == 0
pytest
%endif

%files -n python3-networkx
%if 0%{?rhel} == 0
%doc README.html installed-docs/*
%endif
%license LICENSE.txt
%{python3_sitelib}/networkx*

%if 0%{?rhel} == 0
%files doc
%doc doc/build/html/*
%endif

%changelog
* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 2.6.2-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Aug  4 2021 Petr Lautrbach <plautrba@redhat.com> - 2.6.2-1
- Version 2.6.2

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2.5-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Jerry James <loganjerry@gmail.com> - 2.5-3
- Add -pyyaml patch to fix FTBFS

* Fri Dec 11 2020 Petr Lautrbach <plautrba@redhat.com> - 2.5-2
- Limit BuildRequires to necessary minimum in Red Hat Enterprise Linux
- Skip pytest in Red Hat Enterprise Linux
- Do not build -doc subpackage for Red Hat Enterprise Linux

* Sat Aug 22 2020 Jerry James <loganjerry@gmail.com> - 2.5-1
- Version 2.5
- All patches except -doc have been upstreamed; drop them

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.4-4
- Rebuilt for Python 3.9

* Mon Mar  9 2020 Jerry James <loganjerry@gmail.com> - 2.4-3
- Add -deprecated and -arg-order patches to fix FTBFS with python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov  4 2019 Jerry James <loganjerry@gmail.com> - 2.4-1
- New upstream version
- Drop upstreamed patches: -is, -source-target, -union-find, -cb-iterable,
  -iterable, and -dict-iteration
- Unbundle fonts from the documentation
- Reenable the tests
- Add -test patch

* Wed Sep 11 2019 Jerry James <loganjerry@gmail.com> - 2.3-5
- Add -doc patch to fix building the gallery of examples
- Add -is patch to reduce noise in sagemath
- Add upstream bug fix patches: -source-target, -union-find, -cb-iterable,
  -iterable, and -dict-iteration

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Jerry James <loganjerry@gmail.com> - 2.3-2
- Merge the -test subpackage back into the main package (bz 1708372)

* Sat Apr 27 2019 Jerry James <loganjerry@gmail.com> - 2.3-1
- New upstream version
- Drop upstreamed -abc patch
- Add a -test subpackage (bz 1668197)
- Convert most Requires to Recommends (bz 1668197)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Jerry James <loganjerry@gmail.com> - 2.2-2
- Add -abc patch to quiet warnings

* Sat Oct 13 2018 Jerry James <loganjerry@gmail.com> - 2.2-1
- New upstream version (bz 1600361)
- Drop all patches
- Drop the python2 subpackages (bz 1634570)
- Figure out the BuildRequires all over again (bz 1576805)
- Consolidate BuildRequires so I can tell what is actually on the list
- Drop conditionals for RHEL < 8; this version can never appear there anyway
- Consolidate back to a single package for the same reason
- Temporarily disable tests due to multigraph bug in graphviz > 2.38

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.11-12
- Rebuilt for Python 3.7

* Fri May 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.11-11
- Update graphviz dependency for python2
- Drop graphviz dependency for python3 (graphviz doesn't support python3)

* Fri Mar 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.11-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.11-8
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Orion Poplawski <orion@cora.nwra.com> - 1.11-5
- Add patch to fix sphinx build

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.11-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 14 2016 Jerry James <loganjerry@gmail.com> - 1.11-3
- Change pydot dependencies to pydotplus (bz 1326957)

* Sat Apr  2 2016 Jerry James <loganjerry@gmail.com> - 1.11-2
- Fix gdal and pydot dependencies

* Sat Mar  5 2016 Jerry James <loganjerry@gmail.com> - 1.11-1
- New upstream version
- Drop upstreamed -numpy patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb  1 2016 Jerry James <loganjerry@gmail.com> - 1.10-1
- Comply with latest python packaging guidelines (bz 1301767)

* Tue Dec  1 2015 Jerry James <loganjerry@gmail.com> - 1.10-1
- New upstream version
- Update URLs
- Add -numpy patch to fix test failure

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Jerry James <loganjerry@gmail.com> - 1.9.1-3
- Note bundled jquery

* Tue Oct  7 2014 Jerry James <loganjerry@gmail.com> - 1.9.1-2
- Fix python3-networkx-drawing subpackage (bz 1149980)
- Fix python(3)-geo subpackage

* Mon Sep 22 2014 Jerry James <loganjerry@gmail.com> - 1.9.1-1
- New upstream version
- Fix license handling

* Thu Jul 10 2014 Jerry James <loganjerry@gmail.com> - 1.9-2
- BR python-setuptools

* Tue Jul  8 2014 Jerry James <loganjerry@gmail.com> - 1.9-1
- New upstream version
- Drop upstreamed -test-rounding-fix patch
- Upstream no longer bundles python-decorator; drop the workaround

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.8.1-13
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Mar 13 2014 Pádraig Brady <pbrady@redhat.com> - 1.8.1-12
- Split to subpackages and support EL6 and EL7

* Thu Oct  3 2013 Jerry James <loganjerry@gmail.com> - 1.8.1-2
- Update project and source URLs

* Fri Aug  9 2013 Jerry James <loganjerry@gmail.com> - 1.8.1-1
- New upstream version

* Mon Jul 29 2013 Jerry James <loganjerry@gmail.com> - 1.8-1
- New upstream version
- Add tex-preview BR for documentation

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug  6 2012 Jerry James <loganjerry@gmail.com> - 1.7-1
- New upstream version

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Jerry James <loganjerry@gmail.com> - 1.6-2
- Mass rebuild for Fedora 17

* Mon Nov 28 2011 Jerry James <loganjerry@gmail.com> - 1.6-1
- New upstream version
- Do not use bundled python-decorator
- Remove Requires: ipython, needed by one example only
- Clean junk files left in /tmp

* Wed Jun 22 2011 Jerry James <loganjerry@gmail.com> - 1.5-1
- New upstream version
- Drop defattr
- Build documentation

* Sat Apr 23 2011 Jerry James <loganjerry@gmail.com> - 1.4-1
- New upstream version
- Build for both python2 and python3
- Drop BuildRoot, clean script, and clean at start of install script

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan 20 2010 Conrad Meyer <konrad@tylerc.org> - 1.0.1-1
- Bump version to 1.0.1.
- License changed LGPLv2+ -> BSD.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 24 2009 Conrad Meyer <konrad@tylerc.org> - 0.99-3
- Replace __python macros with direct python invocations.
- Disable checks for now.
- Replace a define with global.

* Thu Mar 12 2009 Conrad Meyer <konrad@tylerc.org> - 0.99-2
- License is really LGPLv2+.
- Include license as documentation.
- Add a check section to run tests.

* Sat Dec 13 2008 Conrad Meyer <konrad@tylerc.org> - 0.99-1
- Initial package.
