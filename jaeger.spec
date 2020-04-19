%define debug_package %{nil}
# Packages
%define _agent agent
%define _collector collector
%define _ingester ingester
%define _query query

Name:          jaeger
Version:       1.17.1
Release:       1%{?dist}
Summary:       Jaeger all in one package.
License:       Apache License 2.0

Source0:       https://github.com/jaegertracing/%{name}/releases/download/v%{version}/%{name}-%{version}-linux-amd64.tar.gz
Source1:       %{name}.service
Source2:       %{name}-%{_agent}.service
Source3:       %{name}-%{_collector}.service
Source4:       %{name}-%{_ingester}.service
Source5:       %{name}-%{_query}.service
Source6:       %{name}.yaml
Source7:       %{name}-%{_agent}.yaml
Source8:       %{name}-%{_collector}.yaml
Source9:       %{name}-%{_ingester}.yaml
Source10:      %{name}-%{_query}.yaml
Source11:      %{name}.env
URL:           https://www.jaegertracing.io/
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%prep
%setup -q -n %{name}-%{version}-linux-amd64

%package %{_agent}
Summary: Jaeger tracing %{_agent}.
Conflicts: %{name},%{name}-all-in-one

%package %{_collector}
Summary: Jaeger tracing %{_collector}.
Conflicts: %{name},%{name}-all-in-one

%package %{_ingester}
Summary: Jaeger tracing %{_ingester}.
Conflicts: %{name},%{name}-all-in-one

%package %{_query}
Summary: Jaeger tracing %{_query}.
Conflicts: %{name},%{name}-all-in-one

%description
Jaeger: open source, end-to-end distributed tracing.
Jaeger all-in-one distribution with agent, collector and query.
Monitor and troubleshoot transactions in complex distributed systems.

%description %{_agent}
Jaeger agent is a daemon program that runs on every host and receives tracing data submitted by Jaeger client libraries.

%description %{_collector}
Jaeger collector receives traces from Jaeger agents and runs them through a processing pipeline.

%description %{_ingester}
Jaeger ingester consumes spans from a particular Kafka topic and writes them to a configured storage.

%description %{_query}
Jaeger query service provides a Web UI and an API for accessing trace data.

%build

%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}

install -p -D -m 0755 %{_builddir}/%{name}-%{version}-linux-amd64/%{name}-all-in-one \
                      %{buildroot}%{_bindir}/%{name}
install -p -D -m 0755 %{_builddir}/%{name}-%{version}-linux-amd64/%{name}-agent \
                      %{buildroot}%{_bindir}/%{name}-%{_agent}
install -p -D -m 0755 %{_builddir}/%{name}-%{version}-linux-amd64/%{name}-collector \
                      %{buildroot}%{_bindir}/%{name}-%{_collector}
install -p -D -m 0755 %{_builddir}/%{name}-%{version}-linux-amd64/%{name}-ingester \
                      %{buildroot}%{_bindir}/%{name}-%{_ingester}
install -p -D -m 0755 %{_builddir}/%{name}-%{version}-linux-amd64/%{name}-query \
                      %{buildroot}%{_bindir}/%{name}-%{_query}

install -p -D -m 0644 %{SOURCE1}   %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2}   %{buildroot}%{_unitdir}/%{name}-%{_agent}.service
install -p -D -m 0644 %{SOURCE3}   %{buildroot}%{_unitdir}/%{name}-%{_collector}.service
install -p -D -m 0644 %{SOURCE4}   %{buildroot}%{_unitdir}/%{name}-%{_ingester}.service
install -p -D -m 0644 %{SOURCE5}   %{buildroot}%{_unitdir}/%{name}-%{_query}.service

install -p -D -m 0644 %{SOURCE6}   %{buildroot}%{_sysconfdir}/%{name}/%{name}.yaml
install -p -D -m 0644 %{SOURCE7}   %{buildroot}%{_sysconfdir}/%{name}/%{name}-%{_agent}.yaml
install -p -D -m 0644 %{SOURCE8}   %{buildroot}%{_sysconfdir}/%{name}/%{name}-%{_collector}.yaml
install -p -D -m 0644 %{SOURCE9}   %{buildroot}%{_sysconfdir}/%{name}/%{name}-%{_ingester}.yaml
install -p -D -m 0644 %{SOURCE10}   %{buildroot}%{_sysconfdir}/%{name}/%{name}-%{_query}.yaml

install -p -D -m 0644 %{SOURCE11}   %{buildroot}%{_sysconfdir}/%{name}/%{name}.env

%clean
rm -rf %{buildroot}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
          -c "Jaeger services" %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
getent passwd %{name} >/dev/null && userdel %{name}
getent group %{name} >/dev/null && groupdel %{name}

%post %{_agent}
%systemd_post %{name}-%{_agent}.service

%preun %{_agent}
%systemd_preun %{name}-%{_agent}.service

%postun %{_agent}
%systemd_postun_with_restart %{name}-%{_agent}.service

%post %{_collector}
%systemd_post %{name}-%{_collector}.service

%preun %{_collector}
%systemd_preun %{name}-%{_collector}.service

%postun %{_collector}
%systemd_postun_with_restart %{name}-%{_collector}.service

%post %{_ingester}
%systemd_post %{name}-%{_ingester}.service

%preun %{_ingester}
%systemd_preun %{name}-%{_ingester}.service

%postun %{_ingester}
%systemd_postun_with_restart %{name}-%{_ingester}.service

%post %{_query}
%systemd_post %{name}-%{_query}.service

%preun %{_query}
%systemd_preun %{name}-%{_query}.service

%postun %{_query}
%systemd_postun_with_restart %{name}-%{_query}.service

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/%{name}
%attr(644, root, root) %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}.yaml
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}.env

%files %{_agent}
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/%{name}-%{_agent}
%attr(644, root, root) %{_unitdir}/%{name}-%{_agent}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}-%{_agent}.yaml
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}.env

%files %{_collector}
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/%{name}-%{_collector}
%attr(644, root, root) %{_unitdir}/%{name}-%{_collector}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}-%{_collector}.yaml
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}.env

%files %{_ingester}
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/%{name}-%{_ingester}
%attr(644, root, root) %{_unitdir}/%{name}-%{_ingester}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}-%{_ingester}.yaml
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}.env

%files %{_query}
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/%{name}-%{_query}
%attr(644, root, root) %{_unitdir}/%{name}-%{_query}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}-%{_query}.yaml
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/%{name}.env

%changelog
* Sun Apr 19 2020 Maxim Levchenko <kagbe.leviy@gmail.com> - 1.17.1
- Create spec
